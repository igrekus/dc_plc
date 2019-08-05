<template>
	<tr>
		<td v-for="cell in row_data">{{ cell }}</td>
	</tr>
</template>

<script>
	export default {
		name: "ExportTableRow",
		props: {
			row_data: Array
		},
		data: function () {
		}
	}
</script>

<style scoped>

</style>