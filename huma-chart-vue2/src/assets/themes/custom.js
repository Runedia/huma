import { registerTheme } from 'echarts/core'

var colorPalette = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']
registerTheme('custom', {
    color: colorPalette,
    backgroundColor: '#fef8ef',
    graph: {
        color: colorPalette,
    },
})
