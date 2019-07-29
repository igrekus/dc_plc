<template>
	<div>
		<table>
			<ExportTableHeader :header_data="headers"></ExportTableHeader>
			<ExportTableRow v-for="row in rows" :row_data="row"></ExportTableRow>
		</table>
	</div>
</template>

<script>
	import ExportTableHeader from './ExportTableHeader.vue'
	import ExportTableRow from './ExportTableRow.vue'

	export default {
		props: {
			productIds: Array,
		},
		data: () => {
			return {
				headers: ['col1', 'col2', 'col3'],
			}
		},
		computed: {
			rows: function () {
				let new_rows = [];
				for (let i = 0; i < this.productIds.length; ++i) {
					let row = [];
					for (let j = 0; j < this.headers.length; ++j) {
						row.push(this.productIds.length[i] + ' ' + this.headers[j]);
					}
					new_rows.push(row);
				}
				return new_rows;
			}
		},
		watch: {
			// productIds: {
			// 	handler: function(new_val, old_val)  {
			// 	},
			// }
		},
		components: {
			ExportTableHeader,
			ExportTableRow
		}
	}
</script>

<style scoped>

</style>

