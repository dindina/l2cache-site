const fs = require('fs');
const path = require('path');

const cryptoSrc = fs.readFileSync(path.join(__dirname, 'crypto-minimal.js'), 'utf-8')
  .replace(/exports\.\w+\s*=\s*[^;]+;?/g, '');

const passwordSrc = fs.readFileSync(path.join(__dirname, 'password-encoding.js'), 'utf-8')
  .replace(/exports\.\w+\s*=\s*[^;]+;?/g, '');

let encryptSrc = fs.readFileSync(path.join(__dirname, 'pdf-encrypt-sub.js'), 'utf-8')
  .replace("const { PDFDocument, PDFName, PDFHexString, PDFString, PDFDict, PDFArray, PDFRawStream, PDFNumber } = require('pdf-lib');", "")
  .replace("const { md5, RC4, hexToBytes, bytesToHex } = require('./crypto-minimal');", "")
  .replace("const { encodePasswordLegacy, PasswordEncodingError } = require('./password-encoding');", "")
  .replace(/exports\.\w+\s*=\s*[^;]+;?/g, '');

const bundle = `/**
 * Standalone Browser Bundle for PDF Encryption (RC4 128-bit Standard Security)
 * Client-Side only, 0 dependencies except PDFLib.
 */
(function(global) {
  'use strict';

  // 1. PDFLib Symbols (dynamically resolved)
  let PDFDocument, PDFName, PDFHexString, PDFString, PDFDict, PDFArray, PDFRawStream, PDFNumber;

  function initPDFLibSymbols() {
    const lib = (typeof window !== 'undefined' && window.PDFLib) 
      ? window.PDFLib 
      : (typeof globalThis !== 'undefined' && globalThis.PDFLib 
        ? globalThis.PDFLib 
        : (typeof global !== 'undefined' ? global.PDFLib : null));
    
    if (!lib) {
      throw new Error('PDFLib is not loaded. Please ensure pdf-lib.min.js is included before encrypting.');
    }
    PDFDocument = lib.PDFDocument;
    PDFName = lib.PDFName;
    PDFHexString = lib.PDFHexString;
    PDFString = lib.PDFString;
    PDFDict = lib.PDFDict;
    PDFArray = lib.PDFArray;
    PDFRawStream = lib.PDFRawStream;
    PDFNumber = lib.PDFNumber;
  }

  // 2. Minimal Crypto (MD5 & RC4)
  ${cryptoSrc}

  // 3. Password Encoding
  ${passwordSrc}

  // 4. PDF Encryption Logic
  ${encryptSrc}

  // Bind global export
  const originalEncryptPDF = typeof encryptPDF !== 'undefined' ? encryptPDF : null;
  
  const root = typeof window !== 'undefined' ? window : (typeof globalThis !== 'undefined' ? globalThis : global);
  root.PDFEncrypt = {
    encryptPDF: async function(pdfInput, userPassword, ownerPassword, options) {
      initPDFLibSymbols();
      return originalEncryptPDF(pdfInput, userPassword, ownerPassword, options);
    },
    AlreadyEncryptedError: typeof AlreadyEncryptedError !== 'undefined' ? AlreadyEncryptedError : Error
  };

  // Auto-init symbols if PDFLib is already present on load
  try { initPDFLibSymbols(); } catch(e) {}
})(typeof window !== 'undefined' ? window : this);
`;

fs.writeFileSync(path.join(__dirname, 'pdf-encrypt.bundle.js'), bundle, 'utf-8');
console.log('Successfully generated tools/vendor/pdf-encrypt.bundle.js');
