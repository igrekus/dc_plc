<template>
	<div>{{ product_ids }}<ButtonCounter :count="50"></ButtonCounter></div>
</template>

<script>
	import ButtonCounter from './ExportTable.vue'

	export default {
		name: "ToolRoot",
		data: function () {
			return {
				product_ids: [],
			}
		},
		components: {
			ButtonCounter
		},
	}
</script>

<style scoped>

</style>