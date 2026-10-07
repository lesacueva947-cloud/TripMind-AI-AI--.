const form = document.getElementById('tripForm');
const summaryEl = document.getElementById('summary');
const weatherNoteEl = document.getElementById('weatherNote');
const travelScoreEl = document.getElementById('travelScore');
const insightsListEl = document.getElementById('insightsList');
const packingListEl = document.getElementById('packingList');
const bestTimeToVisitEl = document.getElementById('bestTimeToVisit');
const budgetBreakdownEl = document.getElementById('budgetBreakdown');
const itineraryEl = document.getElementById('itinerary');
const scenarioGridEl = document.getElementById('scenarioGrid');
const mapListEl = document.getElementById('mapList');
const chatBoxEl = document.getElementById('chatBox');
const loadSampleBtn = document.getElementById('loadSample');

function collectFormData() {
  const formData = new FormData(form);
  const interests = formData.getAll('interests');
  return {
    destination: formData.get('destination') || 'Rome',
    days: Number(formData.get('days') || 3),
    budget: Number(formData.get('budget') || 1800),
    travellers: Number(formData.get('travellers') || 2),
    pace: formData.get('pace') || 'balanced',
    weather: formData.get('weather') || 'sunny',
    scenario: formData.get('scenario') || 'comfort',
    interests: interests.length ? interests : ['culture', 'food'],
  };
}

function renderScenarios(scenarios) {
  scenarioGridEl.innerHTML = scenarios
    .map(
      (scenario) => `
        <article class="scenario-card">
          <strong>${scenario.title}</strong>
          <div>${scenario.description}</div>
          <br />
          <div>Stay: ${scenario.stay}</div>
          <div>Budget: €${scenario.total_budget}</div>
        </article>
      `
    )
    .join('');
}

function renderMap(mapPoints) {
  mapListEl.innerHTML = mapPoints.map((point) => `<li>${point}</li>`).join('');
}

function renderTravelQuality(plan) {
  travelScoreEl.innerHTML = `
    <div class="score-ring">${plan.travel_score}/100</div>
    <div class="score-label">Trip fit score</div>
  `;
  insightsListEl.innerHTML = plan.insights.map((item) => `<li>${item}</li>`).join('');
  packingListEl.innerHTML = plan.packing_list.map((item) => `<li>${item}</li>`).join('');
  bestTimeToVisitEl.innerHTML = `
    <div><strong>Best month:</strong> ${plan.best_time_to_visit.month}</div>
    <div>${plan.best_time_to_visit.reason}</div>
  `;
  budgetBreakdownEl.innerHTML = `
    <div><strong>Total:</strong> €${plan.budget_breakdown.total}</div>
    <div><strong>Per day:</strong> €${plan.budget_breakdown.per_day}</div>
    <ul>
      ${Object.entries(plan.budget_breakdown.categories)
        .map(([key, value]) => `<li>${key}: €${value}</li>`)
        .join('')}
    </ul>
  `;
}

function renderChat(chat) {
  chatBoxEl.innerHTML = `
    <strong>Prompt:</strong>
    <div>${chat.prompt}</div>
    <br />
    <strong>Reply:</strong>
    <div>${chat.answer}</div>
  `;
}

function renderItinerary(itinerary) {
  itineraryEl.innerHTML = itinerary
    .map(
      (day) => `
        <article class="day-card">
          <strong>Day ${day.day}</strong>
          <div>${day.theme}</div>
          <ul>
            ${day.activities
              .map(
                (activity) => `
                  <li>
                    <div><strong>${activity.slot}</strong></div>
                    <div>${activity.title}</div>
                    <div>${activity.interest}</div>
                    <small>€${activity.budget_estimate}</small>
                  </li>
                `
              )
              .join('')}
          </ul>
        </article>
      `
    )
    .join('');
}

async function generatePlan() {
  const params = collectFormData();
  const query = new URLSearchParams({
    destination: params.destination,
    days: String(params.days),
    budget: String(params.budget),
    travellers: String(params.travellers),
    pace: params.pace,
    weather: params.weather,
    scenario: params.scenario,
    interests: params.interests.join(','),
  });

  let plan;
  let scenarios;
  try {
    ({ plan, scenarios } = await fetchTripData(query.toString(), (message) => {
      summaryEl.textContent = message;
    }));
  } catch (error) {
    summaryEl.textContent = `Не удалось построить маршрут: ${error.message}`;
    return;
  }

  summaryEl.innerHTML = `<strong>${plan.summary}</strong>`;
  weatherNoteEl.textContent = plan.weather_note;
  renderTravelQuality(plan);
  renderItinerary(plan.itinerary);
  renderScenarios(scenarios);
  renderMap(plan.map_points);
  renderChat(plan.ai_chat);
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  await generatePlan();
});

loadSampleBtn.addEventListener('click', () => {
  form.destination.value = 'Barcelona';
  form.days.value = 4;
  form.budget.value = 2400;
  form.travellers.value = 2;
  form.pace.value = 'balanced';
  form.weather.value = 'sunny';
  form.scenario.value = 'premium';
  form.querySelectorAll('input[name="interests"]').forEach((checkbox) => {
    checkbox.checked = ['culture', 'food', 'nature'].includes(checkbox.value);
  });
  generatePlan();
});

generatePlan();
