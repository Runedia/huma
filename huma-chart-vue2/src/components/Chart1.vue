<template>
    <v-chart class="chart" :option="option" autoresize />
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { TitleComponent, LegendComponent, GridComponent } from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'

use([CanvasRenderer, BarChart, TitleComponent, LegendComponent, GridComponent])

var colorPalette = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']

export default {
    name: 'Chart1', // 연도별개봉영화수
    components: {
        VChart,
    },
    provide: {
        [THEME_KEY]: 'roma',
    },
    data() {
        return {
            option: {
                title: {
                    text: '연도별 개봉 영화 수',
                    left: 'center',
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{b} : {c}',
                },
                xAxis: {
                    type: 'category',
                    data: ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021'],
                },
                yAxis: {
                    type: 'value',
                },
                series: [
                    {
                        data: [145, 167, 187, 192, 228, 280, 409, 557, 693, 752, 730, 251],
                        type: 'bar',
                        label: {
                            show: true,
                            position: 'outside',
                        },
                        itemStyle: {
                            color: function(x) {
                                return colorPalette[x.dataIndex % colorPalette.length]
                            },
                        },
                    },
                ],
            },
        }
    },
}
</script>

<style scoped>
.chart {
    height: 400px;
}
</style>
