<template>
	<button v-on:click="count++">Счётчик кликов — {{ count }}</button>
</template>

<script>
	export default {
		props: ['count'],
		data: function () {
			return {
				count: 0
			}
		}
	}
</script>

<style scoped>

</style>

