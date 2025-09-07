export const themes = {
  cyberpunk: {
    name: 'Cyberpunk Classic',
    colors: {
      'cyber-bg-primary': '#0f172a',
      'cyber-bg-secondary': '#1e293b',
      'cyber-text-primary': '#f1f5f9',
      'cyber-text-accent': '#22d3ee',
      'cyber-accent-primary': '#a855f7',
      'cyber-accent-secondary': '#06b6d4',
      'cyber-error': '#f97316',
      'cyber-success': '#22c55e',
    }
  },
  
  matrix: {
    name: 'Matrix Green',
    colors: {
      'cyber-bg-primary': '#000000',
      'cyber-bg-secondary': '#0a0a0a',
      'cyber-text-primary': '#00ff00',
      'cyber-text-accent': '#00cc00',
      'cyber-accent-primary': '#22c55e',
      'cyber-accent-secondary': '#65a30d',
      'cyber-error': '#ff4444',
      'cyber-success': '#00ff00',
    }
  },
  
  neon: {
    name: 'Neon Blue',
    colors: {
      'cyber-bg-primary': '#0a0a23',
      'cyber-bg-secondary': '#1a1a3a',
      'cyber-text-primary': '#ffffff',
      'cyber-text-accent': '#00d4ff',
      'cyber-accent-primary': '#3b82f6',
      'cyber-accent-secondary': '#06b6d4',
      'cyber-error': '#ff6b6b',
      'cyber-success': '#51cf66',
    }
  }
};

export const applyTheme = (themeName) => {
  const theme = themes[themeName];
  if (!theme) return;

  const root = document.documentElement;
  Object.entries(theme.colors).forEach(([property, value]) => {
    root.style.setProperty(`--${property}`, value);
  });
  
  localStorage.setItem('selected-theme', themeName);
};