<template>
    <v-chart class="chart" :option="option" autoresize />
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'

use([CanvasRenderer, BarChart, TitleComponent, TooltipComponent, GridComponent])

var colorPalette = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']

export default {
    name: 'Chart5', // 관람객 순위 Top 10
    components: {
        VChart,
    },
    provide: {
        [THEME_KEY]: 'custom',
    },
    data() {
        return {
            option: {
                title: {
                    text: '관람객 순위 Top 10',
                    left: 'center',
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        return `${params.name}: ${params.value.toLocaleString()}`
                    },
                },
                xAxis: {
                    type: 'category',
                    data: ['명량', '극한직업', '신과함께-죄와 벌', '국제시장', '베테랑', '도둑들', '7번방의 선물', '암살', '광해, 왕이 된 남자', '신과함께-인과 연'],
                },
                yAxis: {
                    type: 'value',
                    min: '10000000',
                },
                series: [
                    {
                        data: [17614590, 16266337, 14414561, 14263203, 13413509, 12984692, 12812134, 12706663, 12323291, 12277797],
                        type: 'bar',
                        label: {
                            show: true,
                            position: 'outside',
                            formatter: function(val) {
                                return val.value.toLocaleString()
                            },
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
    height: 800px;
}
</style>
