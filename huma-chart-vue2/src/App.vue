<template>
    <div id="app">
        <Chart1></Chart1>
        <br />
        <Chart2></Chart2>
        <br />
        <HelloWorld msg="Welcome to Your Vue.js App" />
        <br />
        <StackedLineChart></StackedLineChart>
    </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import StackedLineChart from './components/StackedLineChart.vue'
import Chart1 from './components/Chart1.vue'
import Chart2 from './components/Chart2.vue'

export default {
    name: 'App',
    components: {
        HelloWorld,
        StackedLineChart,
        Chart1,
        Chart2,
    },
}
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    /* max-width: 800px; */
}
</style>
