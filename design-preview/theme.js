(() => {
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let choice = 'system';
  try { choice = localStorage.getItem('angelo-preview-theme') || 'system'; } catch {}
  if (!['light', 'dark', 'system'].includes(choice)) choice = 'system';
  const apply = () => {
    document.documentElement.dataset.theme = choice === 'system' ? (system.matches ? 'dark' : 'light') : choice;
  };
  apply();
  system.addEventListener('change', apply);
  document.addEventListener('DOMContentLoaded', () => {
    const select = document.querySelector('#theme-choice');
    select.value = choice;
    select.addEventListener('change', () => {
      choice = select.value;
      try { localStorage.setItem('angelo-preview-theme', choice); } catch {}
      apply();
    });
  });
})();
