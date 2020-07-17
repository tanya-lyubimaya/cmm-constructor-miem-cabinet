<template>
  <div class="wrapper">
    <div class="navigation">
      <section class="container">
        <a
          class="navigation-title"
          href="/enter"
          title="База КИМов - Сервис для преподавателей МИЭМ НИУ ВШЭ"
        >
          <h1 class="title">База КИМов</h1>
        </a>
      </section>
    </div>
    <section id="base" class="container">
      <h3 class="title">База КИМов</h3>
      <el-button
        type="primary"
        native-type="submit"
        class="button buttonCreate"
        @click="seen = !seen"
      >Создать КИМ</el-button>

      <div v-if="seen" id="app">
        <el-form id="cmm-name-form" ref="form" :model="form" label-width="120px">
          <div>
            <label for="cmm_name"><p>Название КИМа<span id="star"> *</span></p></label>
            <el-input v-model="form.cmm_name" class="input" name="cmm_name" />
            <div style="margin-top: 1rem">
              <el-button class="buttonCreate" type="primary" native-type="submit" @click="onSubmit">Добавить</el-button>
              <el-button class="buttonCancel" @click="onCancel">Отменить</el-button>
            </div>
          </div>
        </el-form>
      </div>
      <h3 class="title">Мои КИМы</h3>
      <div id="cmms-list-wrapper" v-if="cmms.length > 0">
        <ul>
          <li v-for="cmm of cmms" :key="cmm.spreadsheetName">{{ cmm.spreadsheetName }}</li>
        </ul>
      </div>
      <div v-else>
        <p>У Вас нет КИМов</p>
      </div>
      <h3 class="title">Мои курсы</h3>
      <div id="courses-list-wrapper" v-if="courses.length > 0">
        <ul>
          <li v-for="course of courses" :key="course.courseName">{{ course.courseName }}</li>
        </ul>
      </div>
      <div v-else>
        <p>У Вас нет преподаваемых курсов</p>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        cmm_name: ''
      },
      courses: [],
      cmms: [],
      msg: 'Hello',
      showMessage: false,
      seen: false
    }
  },
  created() {
    this.getCourses()
  },
  methods: {
    onSubmit() {
      this.$message(JSON.stringify(this.form.cmm_name))
      axios
        .post('http://localhost:5000/cmm-name', {
          'cmm_name': this.form.cmm_name
        })
        .then(
          response => {
            console.log(response)
          },
          error => {
            console.log(error)
          }
        )
    },
    onCancel() {
      this.$message({
        message: 'cancel!',
        type: 'warning'
      })
    },
    getCourses() {
      const path = 'http://localhost:5000/user-courses'
      axios.get(path).then(
        res => {
          this.courses = res.data.courses
          this.cmms = res.data.cmms
        },
        error => {
          console.error(error)
        }
      )
    }
  }
}
</script>

<!--
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="http://code.jquery.com/jquery-2.0.2.min.js"></script>
<script src="https://code.jquery.com/jquery-3.2.1.min.js" integrity="sha256-hwg4gsxgFZhOsEEamdOYGBf13FyQuiTwlAQgxVSNgt4=" crossorigin="anonymous"></script>
-->
