// Источник данных для app.js.
// Локально (python server.py) маршрут считает Python-сервер по адресам /api/...
// На GitHub Pages сервера нет, поэтому тот же Python-код из src/
// выполняется прямо в браузере через Pyodide.

const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.js';
const PYTHON_SOURCES = ['__init__.py', 'trip_planner.py', 'web_api.py'];

const serverAvailable = (async () => {
  try {
    const response = await fetch('/api/scenarios');
    const type = response.headers.get('Content-Type') || '';
    return response.ok && type.includes('application/json');
  } catch (error) {
    return false;
  }
})();

let browserPython = null;

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = src;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`не удалось загрузить ${src}`));
    document.head.append(script);
  });
}

async function startBrowserPython() {
  await loadScript(PYODIDE_URL);
  const pyodide = await loadPyodide();
  pyodide.FS.mkdirTree('/home/pyodide/src');

  for (const name of PYTHON_SOURCES) {
    const response = await fetch(`../src/${name}`);
    if (!response.ok) {
      throw new Error(`не удалось загрузить src/${name}`);
    }
    pyodide.FS.writeFile(`/home/pyodide/src/${name}`, await response.text());
  }

  pyodide.runPython(`
import json, sys
sys.path.insert(0, '/home/pyodide')
from src.web_api import scenarios_from_query, trip_plan_from_query
`);
  return pyodide;
}

function getBrowserPython(onStatus) {
  if (!browserPython) {
    onStatus('Загружаем Python в браузере — первое открытие занимает несколько секунд…');
    browserPython = startBrowserPython().catch((error) => {
      browserPython = null; // при следующей попытке загрузить заново
      throw error;
    });
  }
  return browserPython;
}

function callPython(pyodide, functionName, query) {
  pyodide.globals.set('query', query);
  return JSON.parse(pyodide.runPython(`json.dumps(${functionName}(query))`));
}

async function fetchTripData(query, onStatus = () => {}) {
  if (await serverAvailable) {
    const [planResponse, scenariosResponse] = await Promise.all([
      fetch(`/api/trip-plan?${query}`),
      fetch(`/api/scenarios?${query}`),
    ]);
    return {
      plan: await planResponse.json(),
      scenarios: await scenariosResponse.json(),
    };
  }

  const pyodide = await getBrowserPython(onStatus);
  return {
    plan: callPython(pyodide, 'trip_plan_from_query', query),
    scenarios: callPython(pyodide, 'scenarios_from_query', query),
  };
}
