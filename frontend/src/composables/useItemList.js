// frontend/src/composables/useItemList.js

import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';

export function useItemList(options) {
  const {
    apiGetFunction,
    apiDeleteFunction,
    piniaStore,
    piniaDeleteFunction,
    listProperty,      // The property name in the store for the list
    itemKey = 'item',  // The key to access item text
  } = options;

  // Get reactive reference to the list property
  const { [listProperty]: listRef } = storeToRefs(piniaStore);

  onMounted(async () => {
    try {
      const response = await apiGetFunction();
      piniaStore.$patch((state) => {
        state[listProperty] = response.data.map((item) => ({
          id: item.id,
          [itemKey]: item.text,
          completed: false,
        }));
      });
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  });

  async function deleteItem(itemId) {
    try {
      await apiDeleteFunction(itemId);
      piniaDeleteFunction(itemId);
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  }

  return {
    items: listRef,
    deleteItem,
  };
}
