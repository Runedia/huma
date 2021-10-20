<template>
    <v-chart class="chart" :option="option" autoresize />
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { TitleComponent, LegendComponent, TooltipComponent } from 'echarts/components'
import { LabelLayout } from 'echarts/features'
import VChart, { THEME_KEY } from 'vue-echarts'
import cdata from './Chart3.json'

use([CanvasRenderer, PieChart, TitleComponent, LegendComponent, TooltipComponent, LabelLayout])

export default {
    name: 'Chart3', // 영화명 많이 사용된 단어
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
                    text: '영화명 많이 사용된 단어',
                    left: 'center',
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{b} : {c} ({d}%)',
                },
                legend: {
                    type: 'scroll',
                    orient: 'vertical',
                    right: 10,
                    top: 20,
                    bottom: 20,
                    data: cdata.legendData,
                },
                series: [
                    {
                        name: '단어',
                        type: 'pie',
                        radius: '80%',
                        center: ['50%', '50%'],
                        data: cdata.seriesData,
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.5)',
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
