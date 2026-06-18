const { validatePatient } = require('../src/utils/validation');

// Test 1: Valid patient
console.log('\n========== TEST 1: Valid Patient ==========');
const validPatient = {
  name: 'John Doe',
  email: 'john@example.com',
  phone: '+1234567890',
  dateOfBirth: '1990-01-01',
  medicalId: 'MED-12345678',
  address: '123 Main Street, City, Country'
};
const validResult = validatePatient(validPatient);
console.log('Expected: { isValid: true, errors: [] }');
console.log('Got:', validResult);
console.log(validResult.isValid === true ? '✅ PASSED' : '❌ FAILED');

// Test 2: Invalid patient
console.log('\n========== TEST 2: Invalid Patient ==========');
const invalidPatient = {
  name: 'J',
  email: 'not-an-email',
  phone: '123',
  dateOfBirth: '2200-01-01',
  medicalId: 'INVALID',
  address: ''
};
const invalidResult = validatePatient(invalidPatient);
console.log('Expected: { isValid: false, errors: [...] }');
console.log('Got:', invalidResult);
console.log(invalidResult.isValid === false ? '✅ PASSED' : '❌ FAILED');

// Test 3: Missing fields
console.log('\n========== TEST 3: Missing Fields ==========');
const missingFields = {
  name: 'Jane Smith'
};
const missingResult = validatePatient(missingFields);
console.log('Got errors:', missingResult.errors);
console.log(missingResult.errors.length > 0 ? '✅ PASSED' : '❌ FAILED');

// Test 4: Edge cases
console.log('\n========== TEST 4: Edge Cases ==========');
const edgeCases = {
  name: 'Mary-Jane O\'Connor',  // Has hyphen and apostrophe
  email: 'mary.jane@hospital.org',
  phone: '+441234567890',
  dateOfBirth: '1920-05-15',  // Very old but valid (104 years)
  medicalId: 'MED-99999999',
  address: '123 Main St'  // Short but valid (11 chars)
};
const edgeResult = validatePatient(edgeCases);
console.log('Edge cases test (all should be valid):');
console.log('Got:', edgeResult);
console.log(edgeResult.isValid === true ? '✅ PASSED' : '❌ FAILED');

console.log('\n========== SUMMARY ==========');
console.log('All tests completed!');
