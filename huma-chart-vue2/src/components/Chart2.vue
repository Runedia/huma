<template>
    <v-chart class="chart" :option="option" autoresize />
</template>

<script>
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { SunburstChart } from 'echarts/charts'
import { TitleComponent, LegendComponent, GridComponent } from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'

use([CanvasRenderer, SunburstChart, TitleComponent, LegendComponent, GridComponent])

var data = [
    {
        name: '2010',
        children: [
            { name: '드라마', value: 42, children: [{ name: 306177, value: 42 }] },
            { name: '다큐멘터리', value: 20, children: [{ name: 33135, value: 20 }] },
            { name: '코미디', value: 16, children: [{ name: 933392, value: 16 }] },
        ],
    },
    {
        name: '2011',
        children: [
            { name: '드라마', value: 39, children: [{ name: 674598, value: 39 }] },
            { name: '다큐멘터리', value: 32, children: [{ name: 7201, value: 32 }] },
            { name: '코미디', value: 15, children: [{ name: 1011645, value: 15 }] },
        ],
    },
    {
        name: '2012',
        children: [
            { name: '다큐멘터리', value: 29, children: [{ name: 9505, value: 29 }] },
            { name: '드라마', value: 29, children: [{ name: 275114, value: 29 }] },
            { name: '코미디', value: 16, children: [{ name: 2008627, value: 16 }] },
        ],
    },
    {
        name: '2013',
        children: [
            { name: '드라마', value: 35, children: [{ name: 1020457, value: 35 }] },
            { name: '다큐멘터리', value: 23, children: [{ name: 8695, value: 23 }] },
            { name: '코미디', value: 11, children: [{ name: 495367, value: 11 }] },
        ],
    },
    {
        name: '2014',
        children: [
            { name: '드라마', value: 32, children: [{ name: 788098, value: 32 }] },
            { name: '다큐멘터리', value: 31, children: [{ name: 165292, value: 31 }] },
            { name: '멜로/로맨스', value: 7, children: [{ name: 988136, value: 7 }] },
        ],
    },
    {
        name: '2015',
        children: [
            { name: '드라마', value: 38, children: [{ name: 584232, value: 38 }] },
            { name: '다큐멘터리', value: 27, children: [{ name: 5600, value: 27 }] },
            { name: '멜로/로맨스', value: 15, children: [{ name: 176105, value: 15 }] },
        ],
    },
    {
        name: '2016',
        children: [
            { name: '드라마', value: 41, children: [{ name: 457985, value: 41 }] },
            { name: '다큐멘터리', value: 26, children: [{ name: 23385, value: 26 }] },
            { name: '코미디', value: 15, children: [{ name: 554162, value: 15 }] },
        ],
    },
    {
        name: '2017',
        children: [
            { name: '드라마', value: 53, children: [{ name: 654352, value: 53 }] },
            { name: '다큐멘터리', value: 38, children: [{ name: 71322, value: 38 }] },
            { name: '멜로/로맨스', value: 15, children: [{ name: 398115, value: 15 }] },
        ],
    },
    {
        name: '2018',
        children: [
            { name: '드라마', value: 62, children: [{ name: 373489, value: 62 }] },
            { name: '다큐멘터리', value: 35, children: [{ name: 21847, value: 35 }] },
            { name: '코미디', value: 13, children: [{ name: 1727715, value: 13 }] },
        ],
    },
    {
        name: '2019',
        children: [
            { name: '드라마', value: 63, children: [{ name: 450984, value: 63 }] },
            { name: '다큐멘터리', value: 41, children: [{ name: 13092, value: 41 }] },
            { name: '코미디', value: 20, children: [{ name: 944144, value: 20 }] },
        ],
    },
    {
        name: '2020',
        children: [
            { name: '드라마', value: 44, children: [{ name: 121249, value: 44 }] },
            { name: '다큐멘터리', value: 17, children: [{ name: 16061, value: 17 }] },
            { name: '기타', value: 9, children: [{ name: 38681, value: 9 }] },
        ],
    },
    {
        name: '2021',
        children: [
            { name: '드라마', value: 13, children: [{ name: 9538, value: 13 }] },
            { name: '액션', value: 7, children: [{ name: 745481, value: 7 }] },
            { name: '다큐멘터리', value: 6, children: [{ name: 1109, value: 6 }] },
        ],
    },
]

export default {
    name: 'Chart2', // 연도별 장르 Top 3과 관객 수 평균
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
                    text: '연도별 장르 Top 3과 관객 수 평균',
                    left: 'center',
                },
                series: {
                    type: 'sunburst',
                    emphasis: {
                        focus: 'ancestor',
                    },
                    data: data,
                    radius: [0, '80%'],
                    label: {
                        rotate: '0',
                    },
                },
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
