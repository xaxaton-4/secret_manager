const { app, BrowserWindow, Menu, Tray, nativeImage, dialog } = require('electron');
const AutoLaunch = require('auto-launch'); // Добавляем пакет для автозапуска

let tray = null;
let mainWindow = null;
let autoLauncher = null;

// Инициализация автозапуска
function initializeAutoLaunch() {
  try {
    autoLauncher = new AutoLaunch({
      name: 'SecretManager',
      path: app.getPath('exe'),
    });

    // Проверяем текущее состояние автозапуска
    autoLauncher
      .isEnabled()
      .then((isEnabled) => {
        console.log('Автозапуск включен:', isEnabled);
      })
      .catch((err) => {
        console.error('Ошибка при проверке автозапуска:', err);
      });
  } catch (error) {
    console.error('Ошибка инициализации автозапуска:', error);
  }
}

// Включение автозапуска
function enableAutoLaunch() {
  if (!autoLauncher) return;

  autoLauncher
    .enable()
    .then(() => {
      console.log('Автозапуск успешно включен');
      // Можно показать уведомление
      if (tray && !tray.isDestroyed()) {
        tray.displayBalloon({
          title: 'Автозапуск включен',
          content: 'Приложение будет запускаться автоматически при старте системы.',
          iconType: 'info',
        });
      }
    })
    .catch((err) => {
      console.error('Ошибка включения автозапуска:', err);
      dialog.showErrorBox('Ошибка', 'Не удалось включить автозапуск: ' + err.message);
    });
}

// Выключение автозапуска
function disableAutoLaunch() {
  if (!autoLauncher) return;

  autoLauncher
    .disable()
    .then(() => {
      console.log('Автозапуск успешно выключен');
      // Можно показать уведомление
      if (tray && !tray.isDestroyed()) {
        tray.displayBalloon({
          title: 'Автозапуск выключен',
          content: 'Приложение больше не будет запускаться автоматически.',
          iconType: 'info',
        });
      }
    })
    .catch((err) => {
      console.error('Ошибка выключения автозапуска:', err);
      dialog.showErrorBox('Ошибка', 'Не удалось выключить автозапуск: ' + err.message);
    });
}

// Переключение состояния автозапуска
function toggleAutoLaunch() {
  if (!autoLauncher) return;

  autoLauncher
    .isEnabled()
    .then((isEnabled) => {
      if (isEnabled) {
        disableAutoLaunch();
      } else {
        enableAutoLaunch();
      }
    })
    .catch((err) => {
      console.error('Ошибка проверки состояния автозапуска:', err);
    });
}

// Получение текущего состояния автозапуска
function getAutoLaunchStatus(callback) {
  if (!autoLauncher) {
    callback(false);
    return;
  }

  autoLauncher
    .isEnabled()
    .then((isEnabled) => {
      callback(isEnabled);
    })
    .catch((err) => {
      console.error('Ошибка получения статуса автозапуска:', err);
      callback(false);
    });
}

function createWindow() {
  // Создаем окно браузера
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    },
  });

  // Загружаем index.html
  mainWindow.loadFile('./dist/index.html');

  // Открываем DevTools в режиме разработки
  if (process.argv.includes('--dev')) {
    mainWindow.webContents.openDevTools();
  }

  // Обработка закрытия окна
  mainWindow.on('close', (event) => {
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();

      // Показываем уведомление о том, что приложение свернуто в трей
      if (tray && !tray.isDestroyed()) {
        tray.displayBalloon({
          title: 'Приложение свернуто',
          content:
            'Приложение продолжает работать в системном трее. Нажмите на иконку для открытия.',
          iconType: 'info',
        });
      }
    }
  });
}

function createTray() {
  // Создаем иконку для трея
  const icon = nativeImage.createFromPath('./dist/vite.ico');
  tray = new Tray(icon);

  // Обновляем меню при создании
  updateTrayMenu();

  // Всплывающая подсказка
  tray.setToolTip('SecretManager\nДвойной клик - открыть/скрыть');

  // Двойной клик по иконке в трее
  tray.on('double-click', () => {
    toggleWindow();
  });

  // Клик по иконке (для macOS)
  if (process.platform === 'darwin') {
    tray.on('click', () => {
      toggleWindow();
    });
  }
}

function updateTrayMenu() {
  // Получаем текущий статус автозапуска для отображения в меню
  getAutoLaunchStatus((isAutoLaunchEnabled) => {
    const contextMenu = Menu.buildFromTemplate([
      {
        label: 'Открыть/скрыть приложение',
        click: () => {
          toggleWindow();
        },
      },
      { type: 'separator' },
      {
        label: 'Автозапуск при старте системы',
        type: 'checkbox',
        checked: isAutoLaunchEnabled,
        click: () => {
          toggleAutoLaunch();
          // Обновляем меню через короткую задержку
          setTimeout(updateTrayMenu, 100);
        },
      },
      { type: 'separator' },
      {
        label: 'О программе',
        click: () => {
          showAbout();
        },
      },
      { type: 'separator' },
      {
        label: 'Выход',
        click: () => {
          quitApp();
        },
      },
    ]);

    if (tray && !tray.isDestroyed()) {
      tray.setContextMenu(contextMenu);
    }
  });
}

function toggleWindow() {
  if (!mainWindow) return;

  if (mainWindow.isVisible()) {
    mainWindow.hide();
  } else {
    showWindow();
  }
}

function showWindow() {
  if (mainWindow) {
    mainWindow.show();
    mainWindow.focus();

    // На macOS активируем приложение в доке
    if (process.platform === 'darwin') {
      app.dock.show();
    }
  }
}

function showAbout() {
  getAutoLaunchStatus((isAutoLaunchEnabled) => {
    const autoLaunchStatus = isAutoLaunchEnabled ? 'включен' : 'выключен';

    dialog.showMessageBox(mainWindow, {
      type: 'info',
      title: 'О программе',
      message: 'SecretManager',
      detail: `Приложение работает в системном трее.\n\nДля открытия приложения используйте:\n• Двойной клик по иконке в трее\n• Пункт "Открыть приложение" в меню трея\n\nАвтозапуск: ${autoLaunchStatus}`,
    });
  });
}

function quitApp() {
  // Устанавливаем флаг выхода
  app.isQuitting = true;

  // Показываем подтверждение выхода
  const result = dialog.showMessageBoxSync(mainWindow, {
    type: 'question',
    buttons: ['Да, выйти', 'Нет, остаться'],
    defaultId: 1,
    title: 'Подтверждение выхода',
    message: 'Вы действительно хотите выйти из приложения?',
    detail: 'Приложение будет полностью закрыто.',
  });

  if (result === 0) {
    // Пользователь подтвердил выход
    if (mainWindow) {
      mainWindow.destroy();
    }
    if (tray && !tray.isDestroyed()) {
      tray.destroy();
    }
    app.quit();
  } else {
    // Пользователь отменил выход
    app.isQuitting = false;
  }
}

app.whenReady().then(() => {
  createWindow();
  createTray();

  // Инициализируем автозапуск после создания окна
  initializeAutoLaunch();

  // На macOS скрываем иконку в доке если окно скрыто
  if (process.platform === 'darwin') {
    app.dock.hide();
  }
});

// Обработка события перед закрытием приложения
app.on('before-quit', () => {
  app.isQuitting = true;
});

app.on('window-all-closed', (event) => {
  // Не закрываем приложение на macOS при закрытии окон
  if (process.platform !== 'darwin') {
    event.preventDefault();
  }
});

app.on('activate', () => {
  // На macOS пересоздаем окно при клике на иконку в доке
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  } else {
    showWindow();
  }
});

// Блокируем multiple instances
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    // Если пользователь пытается запустить вторую копию, фокусируемся на существующем окне
    if (mainWindow) {
      showWindow();
    }
  });
}
