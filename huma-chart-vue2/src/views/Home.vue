<template>
    <div class="home">
        <div id="nav">
            <h1 style="font-family: 'kodia', cursive;">HUMA 팀. 아모른직다</h1>
            <router-link to="/Chart1">연도별 개봉 영화 수</router-link>
            <br />
            <router-link to="/Chart2">연도별 장르 Top 3와 관객 수 평균</router-link>
            <br />
            <router-link to="/Chart3">영화명 많이 사용된 단어</router-link>
            <br />
            <router-link to="/Chart4">영화명 많이 사용된 단어 &#40;R18+ &#41;</router-link>
            <br />
            <router-link to="/Chart5">관람객 순위 Top 10</router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Page_Home',
    components: {},
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
