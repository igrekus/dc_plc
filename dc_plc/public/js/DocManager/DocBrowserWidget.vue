<template>
	<div>
		<el-button @click="dialogTableVisible = true">
			new doc
		</el-button>

		<el-dialog title="Новый документ" :visible.sync="dialogTableVisible">
			<doc-file-dialog v-bind:formData="formData"></doc-file-dialog>
		</el-dialog>

		<el-input
				placeholder="Filter keyword"
				v-model="filterText">
		</el-input>

		<div class="custom-tree-container">
			<div class="block">
				<el-tree
						:data="data"
						show-checkbox
						node-key="id"
						default-expand-all
						:expand-on-click-node="false">
					<span class="custom-tree-node" slot-scope="{ node, data }">
						<span>{{ node.label }}</span>
						<span>
							<el-button
									type="text"
									size="mini"
									@click="() => append(data)">+
							</el-button>
							<el-button
									type="text"
									size="mini"
									@click="() => remove(node, data)">-
							</el-button>
						</span>
					</span>
				</el-tree>
			</div>
		</div>
	</div>
</template>

<script>
	import DocFileDialog from './DocFileDialog.vue'
	let id = 1000;

	export default {
		name: "DocBrowserWidget",
		data() {
			const data = [
				{
					id: 1,
					label: 'root 1',
					children: [{
						id: 4,
						label: 'Level two 1-1',
						children: [{
							id: 9,
							label: 'Level three 1-1-1'
						}, {
							id: 10,
							label: 'Level three 1-1-2'
						}]
					}]
				},
				{
					id: 2,
					label: 'root 2',
					children: [{
						id: 5,
						label: 'Level two 2-1'
					}, {
						id: 6,
						label: 'Level two 2-2'
					}]
				}, {
					id: 3,
					label: 'root 3',
					children: [{
						id: 7,
						label: 'Level two 3-1'
					}, {
						id: 8,
						label: 'Level two 3-2'
					}]
				}];
			return {
				data: JSON.parse(JSON.stringify(data)),
				filterText: '',
				dialogTableVisible: false,
				formData: {
					name: '',
					type: '',
					subtype: '',
					note: 'note',
					optional: {
						num: 'num',
						int_num: 'int num',
						date_approve: null,
						date_archive: null,
					},
				}
			}
		},

		methods: {
			append(data) {
				const newChild = {id: id++, label: 'testtest', children: []};
				if (!data.children) {
					this.$set(data, 'children', []);
				}
				data.children.push(newChild);
			},

			remove(node, data) {
				const parent = node.parent;
				const children = parent.data.children || parent.data;
				const index = children.findIndex(d => d.id === data.id);
				children.splice(index, 1);
			},

			newDocument() {
				console.log('new doc');
			}
		},
		components: {
			DocFileDialog,
		},
	}
</script>

<style scoped>
	.custom-tree-node {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: space-between;
		font-size: 14px;
		padding-right: 8px;
	}
</style>