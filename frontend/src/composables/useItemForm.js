// frontend/src/composables/useItemForm.js

/**
 * Manages adding items with validation, API call, and state update.
 *
 * @param {Function} apiAddFunction - The API function to call when adding an item.
 * @param {Function} piniaAddFunction - The function to add the item to the Pinia store.
 * @param {string} inputProperty - The name of the input field.
 * @param {string} validationErrorMessage - Custom error message for validation.
 * 
 * @typedef {Object} ReactiveItem
 * @property {string} inputProperty - The reactive property for input management.
 * 
 * @function addItemAndClear
 * @description Validates the input, calls the API function to add the item, updates the Pinia store, and clears the input field.
 */


import { reactive } from 'vue';

export function useItemForm(options) {
  const {
    apiAddFunction,
    piniaAddFunction,
    inputProperty,
    validationErrorMessage,
  } = options;

  const item = reactive({ [inputProperty]: '' });

  async function addItemAndClear() {
    const inputValue = item[inputProperty];

    if (!inputValue || typeof inputValue !== 'string' || inputValue.trim().length === 0) {
      console.error(validationErrorMessage || 'Invalid input: input is either empty or not a string.');
      return;
    }

    try {
      const response = await apiAddFunction({ text: inputValue.trim() });
      const addedItem = response.data;

      // Add item to Pinia store using the backend-assigned ID
      piniaAddFunction(addedItem);

      // Clear input field
      item[inputProperty] = '';
    } catch (error) {
      console.error('Error adding item:', error);
    }
  }

  return {
    item,
    addItemAndClear,
  };
}
