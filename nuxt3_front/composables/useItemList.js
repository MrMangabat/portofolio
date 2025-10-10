// composables/useItemList.js
import { onMounted, toRaw, watch } from 'vue';
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
      
      // 🧪 DEBUG: Test direct fetch first
      try {
        console.log('🧪 Testing direct fetch...');
        const directResponse = await fetch('http://localhost:8080/corrections?correction_type=skill');
        const directData = await directResponse.json();
        console.log('🧪 Direct fetch success:', directData.length, 'items');
      } catch (directError) {
        console.error('🧪 Direct fetch failed:', directError);
      }
      
      const result = await apiGetFunction();
      
      console.log('✅ useFetch Result:', result);
      console.log('📦 Result.pending.value:', result.pending?.value);
      console.log('📦 Result.error.value:', result.error?.value);
      console.log('📦 Result.data.value:', result.data?.value);
      
      // ⚠️ Wait for useFetch to complete if still pending
      if (result.pending?.value === true) {
        console.log('⏳ Request is still pending, waiting...');
        await new Promise((resolve) => {
          const unwatch = watch(result.pending, (isPending) => {
            if (!isPending) {
              unwatch();
              resolve();
            }
          });
        });
        console.log('✅ Request completed, data ready');
      }
      
      // Check for errors
      if (result.error?.value) {
        console.error('❌ API Error:', result.error.value);
        return;
      }
      
      // Get the actual data
      let responseData = null;
      if (result.data?.value) {
        responseData = toRaw(result.data.value);
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
      } else {
        console.warn('⚠️ No data received');
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