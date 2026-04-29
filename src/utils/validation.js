/**
 * Patient validation utilities
 * Issue #34 - Input validation for patient registration
 */

// Validation rules
const VALIDATION_RULES = {
  name: {
    pattern: /^[A-Za-z\s\-']{2,100}$/,
    message: 'Name must be 2-100 characters (letters, spaces, hyphens, apostrophes only)'
  },
  email: {
    pattern: /^[^\s@]+@([^\s@.,]+\.)+[^\s@.,]{2,}$/,
    message: 'Please enter a valid email address'
  },
  phone: {
    pattern: /^\+?[1-9]\d{1,14}$/,
    message: 'Phone must be in E.164 format (e.g., +1234567890)'
  },
  dateOfBirth: {
    validate: (date) => {
      const dob = new Date(date);
      const today = new Date();
      const age = today.getFullYear() - dob.getFullYear();
      return dob <= today && age <= 120 && age >= 0;
    },
    message: 'Date of birth must be valid and age between 0-120 years'
  },
  medicalId: {
    pattern: /^MED-\d{8}$/,
    message: 'Medical ID must follow format: MED-XXXXXXXX (8 digits)'
  },
  address: {
    validate: (addr) => addr && addr.trim().length >= 5 && addr.trim().length <= 200,
    message: 'Address must be 5-200 characters'
  }
};

/**
 * Validate patient registration data
 * @param {Object} patientData - Patient information
 * @returns {Object} { isValid: boolean, errors: Array }
 */
function validatePatient(patientData) {
  const errors = [];

  // Check each required field
  const requiredFields = ['name', 'email', 'phone', 'dateOfBirth', 'medicalId', 'address'];
  
  for (const field of requiredFields) {
    if (!patientData[field]) {
      errors.push(`${field} is required`);
      continue;
    }
    
    const rule = VALIDATION_RULES[field];
    if (!rule) continue;
    
    let isValid = true;
    
    if (rule.pattern) {
      isValid = rule.pattern.test(patientData[field]);
    } else if (rule.validate) {
      isValid = rule.validate(patientData[field]);
    }
    
    if (!isValid) {
      errors.push(rule.message);
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors: errors
  };
}

module.exports = { validatePatient, VALIDATION_RULES };
