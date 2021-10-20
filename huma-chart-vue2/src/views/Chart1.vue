<template>
    <div>
        <div id="nav">
            <router-link to="/"><mdicon name="home" /> </router-link>
        </div>
        <Chart1></Chart1>
    </div>
</template>

<script>
import Chart1 from '@/components/Chart1.vue'

export default {
    name: 'Page_Chart1',
    components: {
        Chart1,
    },
}
</script>

<style>
#nav {
    padding: 30px;
}

#nav a {
    margin: 30px;
}

#nav a:link,
a:visited {
    background-color: white;
    color: black;
    border: 2px solid #be1824;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    width: 300px;
}

#nav a:hover,
a:active {
    background-color: #be1824;
    color: white;
}
</style>
