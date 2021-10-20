<template>
    <v-chart class="chart" :option="option" autoresize @mouseover="onMouseOver" />
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, PieChart } from 'echarts/charts'
import { TooltipComponent, GridComponent, LegendComponent, MarkLineComponent, TitleComponent } from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'
import data from './Chart2.json'

use([CanvasRenderer, BarChart, PieChart, TooltipComponent, GridComponent, LegendComponent, MarkLineComponent, TitleComponent])

export default {
    name: 'Chart2_v2', // 연도별 장르 Top 3과 관객 수 평균
    components: {
        VChart,
    },
    provide: {
        [THEME_KEY]: 'custom',
    },
    data() {
        return {
            option: {
                title: [
                    {
                        left: 'center',
                        text: '연도별 장르 Top 3',
                    },
                    {
                        left: '15%',
                        text: '연도별 관객 수 평균',
                    },
                ],
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow',
                    },
                },
                legend: {
                    right: 10,
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true,
                },
                xAxis: [
                    {
                        type: 'category',
                        data: data.category,
                        triggerEvent: true,
                    },
                ],
                yAxis: [
                    {
                        type: 'value',
                    },
                ],
                series: [...data.series].concat([
                    {
                        name: '관객 수',
                        type: 'pie',
                        center: ['20%', '20%'],
                        radius: '30%',
                        label: { show: false },
                        z: 100,
                        data: data.sub_series['2010'],
                    },
                ]),
            },
        }
    },
    methods: {
        onMouseOver: function(params) {
            if (params.seriesType == 'pie') {
                this.$data.option.tooltip.trigger = 'item'
            } else {
                this.$data.option.tooltip.trigger = 'axis'
            }

            if (params.seriesType == 'bar') {
                let name = params.name
                if (name) {
                    this.$data.option.series = [...data.series].concat([
                        {
                            name: '평균 관객 수',
                            type: 'pie',
                            center: ['20%', '20%'],
                            radius: '30%',
                            label: { show: false },
                            z: 100,
                            data: data.sub_series[name],
                        },
                    ])
                }
            }
        },
    },
}
</script>

<style scoped>
.chart {
    height: 800px;
}
</style>
