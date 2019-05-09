<template>
    <div class="board">
        <el-col :span="14" class="sub-header">排行榜</el-col>
        <el-col :span="10" class="genre">
        <el-select v-model="genre" placeholder="请选择">
            <el-option
            v-for="item in genres"
            :key="item.value"
            :label="item.label"
            :value="item.value">
            </el-option>
        </el-select>
        </el-col>
        <div class=boarding-list>
            <p v-for="(movie, index) in boardingRes" :key="index" @click="selectMovie(movie)" class="title">{{movie.title}}</p>
        </div>
        <el-col class="sub-header">口碑榜</el-col>
        <div class=boarding-list>
            <p v-for="(movie, index) in totalRes" :key="index" @click="selectMovie(movie)" class="title">{{movie.title}}</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Boarding",
        props: ["movieList"],
        data() {
            return {
                genre: "",
                genres: [],
                boardingRes: [],
                totalRes: []
            }
        },

        mounted: async function() {
            this.genres = await axios.get('/api/genres').then((response) => {
                var genreSet = response.data
                var genreOp = []
                genreSet.forEach(element => {
                    genreOp.push({"value": element, "label": element})
                })
                return genreOp
            })
            this.genre = this.genres[0].value
            this.totalRes = await axios.get('/api/genre').then((response) => {
                return response.data
            })
        },

        methods: {
            selectMovie: function(movie) {
                this.$emit("titleSearchChanged", movie.title)
            }
        },

        watch: {
            genre: function() {
                axios.get('/api/genre=' + this.genre).then((response) => {
                    this.boardingRes = response.data
                })
            }
        }
    }
</script>

<style scoped>
.board {
    -webkit-user-select: none
}
.sub-header {
    text-align: left;
    padding-left: 12px;
    padding-top: 25px;
    font-size: 20px;
    opacity: 1;
    line-height: 1.4;
    font-weight: 500;
    color: darkcyan
  }
  .genre {
    opacity: 1;
    line-height: 1.4;
    font-weight: 300;
    padding-top: 20px;
    float: right;
    padding-right: 8px;
  }
  .boarding-list {
    opacity: 1;
    line-height: 1.4;
    font-weight: 500;
    text-align: left;
    float: left;
    padding: 12px;
  }
  .title {
    cursor: pointer;
  }
</style>