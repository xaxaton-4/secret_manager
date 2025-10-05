// Функция для шифрования текста
export async function encryptAES(text: string, password: string) {
  try {
    // Кодируем текст и пароль
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const passwordBuffer = encoder.encode(password);

    // Создаем ключ из пароля
    const keyMaterial = await window.crypto.subtle.importKey(
      'raw',
      passwordBuffer,
      'PBKDF2',
      false,
      ['deriveKey'],
    );

    // Генерируем соль
    const salt = window.crypto.getRandomValues(new Uint8Array(16));

    // Создаем ключ AES с помощью PBKDF2
    const key = await window.crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: salt,
        iterations: 100000,
        hash: 'SHA-256',
      },
      keyMaterial,
      { name: 'AES-GCM', length: 256 },
      false,
      ['encrypt', 'decrypt'],
    );

    // Генерируем IV (Initialization Vector)
    const iv = window.crypto.getRandomValues(new Uint8Array(12));

    // Шифруем данные
    const encrypted = await window.crypto.subtle.encrypt(
      {
        name: 'AES-GCM',
        iv: iv,
      },
      key,
      data,
    );

    // Объединяем соль, IV и зашифрованные данные
    const result = new Uint8Array(salt.length + iv.length + encrypted.byteLength);
    result.set(salt, 0);
    result.set(iv, salt.length);
    result.set(new Uint8Array(encrypted), salt.length + iv.length);

    // Конвертируем в base64 для удобства хранения
    return btoa(String.fromCharCode(...result));
  } catch (error) {
    return '';
  }
}

// Функция для расшифрования текста
export async function decryptAES(encryptedData: string, password: string) {
  try {
    // Декодируем из base64
    const encryptedBuffer = Uint8Array.from(atob(encryptedData), (c) => c.charCodeAt(0));

    // Извлекаем соль, IV и зашифрованные данные
    const salt = encryptedBuffer.slice(0, 16);
    const iv = encryptedBuffer.slice(16, 28);
    const encrypted = encryptedBuffer.slice(28);

    // Кодируем пароль
    const encoder = new TextEncoder();
    const passwordBuffer = encoder.encode(password);

    // Создаем ключ из пароля
    const keyMaterial = await window.crypto.subtle.importKey(
      'raw',
      passwordBuffer,
      'PBKDF2',
      false,
      ['deriveKey'],
    );

    // Восстанавливаем ключ AES
    const key = await window.crypto.subtle.deriveKey(
      {
        name: 'PBKDF2',
        salt: salt,
        iterations: 100000,
        hash: 'SHA-256',
      },
      keyMaterial,
      { name: 'AES-GCM', length: 256 },
      false,
      ['encrypt', 'decrypt'],
    );

    // Расшифровываем данные
    const decrypted = await window.crypto.subtle.decrypt(
      {
        name: 'AES-GCM',
        iv: iv,
      },
      key,
      encrypted,
    );

    // Декодируем в текст
    const decoder = new TextDecoder();
    return decoder.decode(decrypted);
  } catch (error) {
    return '';
  }
}
