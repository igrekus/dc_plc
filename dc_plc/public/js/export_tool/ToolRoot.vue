<template>
	<div><ExportTable v-bind:productIds="product_ids"></ExportTable></div>
</template>

<script>
	import ExportTable from './ExportTable.vue'

	export default {
		name: "ToolRoot",
		data: () => {
			return {
				product_ids: [],
			}
		},
		components: {
			ExportTable
		},
	}
</script>

<style scoped>

</style>