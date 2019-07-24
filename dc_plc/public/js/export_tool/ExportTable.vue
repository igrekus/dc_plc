<template>
	<div>
		<table>
			<thead>
			<tr>
				<th v-for="header in headers">{{ header }}</th>
			</tr>
			<tr v-for="id in productIds">
				<td v-for="header in headers">{{ id }}</td>
			</tr>
			</thead>
		</table>
		<div>
			{{ row_data }}
		</div>
	</div>
</template>

<script>
	export default {
		props: {
			productIds: Array,
		},
		data: () => {
			return {
				headers: ['col1', 'col2', 'col3'],
				row_data: [],
			}
		},
		computed: {
			rd: () => {
				return 'lol';
			}
		},
		watch: {
			productIds: {
				handler: (new_val, old_val) => {
					console.log(this.row_data);
				},
				deep: true
			}
		}
	}
</script>

<style scoped>

</style>

