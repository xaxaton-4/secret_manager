import CryptoJS from 'crypto-js';

export function encryptAES(plaintext: string, secretKey: string) {
  const encrypted = CryptoJS.AES.encrypt(plaintext, secretKey);
  return encrypted.toString();
}

export function decryptAES(ciphertext: string, secretKey: string) {
  const decrypted = CryptoJS.AES.decrypt(ciphertext, secretKey);
  return decrypted.toString(CryptoJS.enc.Utf8);
}
