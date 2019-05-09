<template>
  <div>
    <el-container>
      <el-header>
        <el-col :span="6">
          <el-input v-model="search" placeholder="请输入需要检索的内容"></el-input>
        </el-col>
        <el-col :span="2">
          <el-select v-model="command" placeholder="请选择">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-col>
        <el-col :span="10" class="header-text">My Movie List</el-col>
        <el-col :span="6">
          <div class="block">
            <el-pagination
              @current-change="handleCurrentChange"
              layout="prev, pager, next"
              :current-page="currentPage"
              :page-size="pageSize"
              :total="totalMovie">
            </el-pagination>
        </div>
        </el-col>
      </el-header>
      <el-container>
        <el-aside>
          <div class="boarding">
            <Boarding :movieList="movies" @titleSearchChanged="searchTitle($event)" />
          </div>
        </el-aside>
        <el-main>
            <el-row v-for="(movie,index) in res" :key="index">
              <el-col :span=24>
                <MovieCard :detail = "movie" />
              </el-col>
            </el-row>
        </el-main>
      </el-container>
    </el-container>  
  </div>
</template>

<script>
import MovieCard from './MovieCard'
import Boarding from './Boarding'
export default {
  name: 'MovieList',
  components: {
      MovieCard,
      Boarding
    },
  data () {
    return {
      movies: [],
      currentPage: 0,
      pageSize: 10,
      totalMovie: 0,
      search: '',
      oldSearch: '',
      command: '按名称',
      options: [{
          value: '按名称',
          label: '按名称'
        }, {
          value: '按导演',
          label: '按导演'
        }, {
          value: '按演员',
          label: '按演员'
        },{
          value: '按简介',
          label: '按简介'
        }],
      genre: "",
      currentPageMovies: []
    }
  },

  mounted: function() {
    this.currentPage = 1
  },

  methods: {
    handleCurrentChange(val) {
      this.currentPage = val
    },
    searchTitle(movieTitle) {
      this.command = "按名称"
      this.search = movieTitle
    },
    searchMovies() {
      if(this.search != this.oldSearch) {
        this.currentPage = 1
        this.oldSearch = this.search
      }
      var searchUrl = ''
      var params = new URLSearchParams()
      if(this.search === '') {
        searchUrl = '/api/page=' + this.currentPage
        axios.get(searchUrl).then((response) => {
          this.currentPageMovies = response.data.movies
          this.totalMovie = response.data.count
        })
        return
      }
      else if(this.command === "按名称") {
        searchUrl = '/api/title&page'
        params.append('title', this.search)
        params.append('page', this.currentPage)
      }
      else if(this.command === "按导演") {
        searchUrl = '/api/directors&page'
        params.append('directors', this.search)
        params.append('page', this.currentPage)
      }
      else if(this.command === "按演员") {
        searchUrl = '/api/casts&page'
        params.append('casts', this.search)
        params.append('page', this.currentPage)
      }
      else {
        searchUrl = '/api/summary&page'
        params.append('text', this.search)
        params.append('page', this.currentPage)
      }
      axios.post(searchUrl, params).then((response) => {
          this.currentPageMovies = response.data.movies
          this.totalMovie = response.data.count
      })
    }
  },

  computed: {
    res() {
      var result = this.currentPageMovies
      return result
    }
  },

  watch: {
    currentPage: function() {
      this.searchMovies()
    },
    search: function() {
      this.searchMovies()
    },
    command: function() {
      this.searchMovies()
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  }

  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }

  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
    font-size: 20px;
  }

  .header-text {
    font-size: 28px;
    font-family: 'Times New Roman', Times, serif
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
    width: 25%;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 160px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }

  .block {
    float:right;
    padding-top:15px
  }

  .el-dropdown-link {
    cursor: pointer;
    color: white;
  }

  .el-icon-arrow-down {
    font-size: 12px;
  }

  .boarding {
    padding-left: 8px;
  }
</style>
