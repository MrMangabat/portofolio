// composables/useItemList.js
import { onMounted, toRaw } from 'vue';
import { storeToRefs } from 'pinia';

export function useItemList(options) {
  const {
    apiGetFunction,
    apiDeleteFunction,
    piniaStore,
    piniaDeleteFunction,
    listProperty,
  } = options;

  const storeRefs = storeToRefs(piniaStore);
  const items = storeRefs[listProperty];
  
  console.log('🔧 Pinia setup:', {
    listProperty,
    itemsExists: !!items,
    itemsLength: items?.value?.length || 0
  });

  const fetchItems = async () => {
    try {
      console.log('🔍 Starting API fetch...');
      
      const result = await apiGetFunction();
      
      console.log('✅ useFetch Result:', result);
      console.log('📦 Result.data:', result.data);
      console.log('📦 Result.data.value:', result.data?.value);
      
      // ✅ Properly unwrap reactive data from useFetch
      let responseData = null;
      
      if (result.data && result.data.value) {
        // Handle reactive ref with value
        responseData = toRaw(result.data.value);  // ✅ Unwrap proxy
      } else if (result.data) {
        // Handle direct data
        responseData = toRaw(result.data);        // ✅ Unwrap proxy
      }
      
      console.log('🎯 Final data to process:', responseData);
      console.log('📈 Data type:', Array.isArray(responseData) ? 'Array' : typeof responseData);
      console.log('📈 Data length:', responseData?.length);
      
      if (responseData && Array.isArray(responseData)) {
        console.log('🏪 Before store update:', piniaStore[listProperty]?.length || 0);
        
        piniaStore.$patch((state) => {
          state[listProperty] = responseData.map((item) => ({
            id: item.id,
            text: item.text,
            type: item.type,
            completed: false,
          }));
        });
        
        console.log('🏪 After store update:', piniaStore[listProperty]?.length || 0);
        console.log('🔍 Reactive ref updated:', items?.value?.length || 0);
      } else {
        console.warn('⚠️ Data is not an array:', responseData);
      }
    } catch (error) {
      console.error('❌ Error fetching items:', error);
    }
  };

  // ✅ Only call on client-side mount
  onMounted(() => {
    fetchItems();
  });

  async function deleteItem(itemId) {
    try {
      await apiDeleteFunction(itemId);
      piniaDeleteFunction(itemId);
    } catch (error) {
      console.error('❌ Error deleting item:', error);
    }
  }

  return {
    items,
    deleteItem,
    fetchItems,
  };
}