<template>
    <div>
        <div id="nav">
            <router-link to="/"><mdicon name="home" /> </router-link>
        </div>
        <Chart5></Chart5>
    </div>
</template>

<script>
import Chart5 from '@/components/Chart5.vue'

export default {
    name: 'Page_Chart5',
    components: {
        Chart5,
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
