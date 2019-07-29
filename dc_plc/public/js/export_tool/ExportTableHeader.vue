<template>
	<thead>
	<tr>
		<th v-for="header in header_data">{{ header }}</th>
	</tr>
	</thead>

</template>

<script>
	export default {
		name: "ExportTableHeader",
		props: {
			header_data: Array
		},
		data: function () {
		}
	}
</script>

<style scoped>

</style>