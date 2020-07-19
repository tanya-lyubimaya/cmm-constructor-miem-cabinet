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
          <li v-for="(cmm, index) in cmms" :key="cmm.spreadsheetName" @click="toggleActive(index)">{{ cmm.spreadsheetName }}
            <div v-if="seenCMM.includes(index)">
              <el-button class="buttonCreate" type="primary" @click="onCancel">Открыть КИМ</el-button>
              <el-button class="buttonCancel" @click="onCancel">Сформировать билеты</el-button>
              <el-button class="buttonCancel" @click="onCancel">Посмотреть билеты</el-button>
              <el-button class="buttonCancel" @click="onCancel">Раздать билеты</el-button>
              <el-button class="buttonCancel" @click="onCancel">Удалить билеты</el-button>
              <el-button class="buttonCancel" @click="onDeleteCMM(index, cmm.spreadsheetId)">Удалить КИМ</el-button>
            </div>
          </li>
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
import Vue from 'vue'

export default {
  data() {
    return {
      form: {
        cmm_name: ''
      },
      courses: [],
      cmms: [],
      msg: 'Hello',
      seen: false,
      seenCMM: [],
      downloadedCourses: false
    }
  },
/*beforeRouteEnter: function(to, from, next) {
  console.log('before enter')
  //vm => vm.getCourses()
  next(vm => vm.getCourses())
  //next()
},*/
created() {
  this.getCourses()
},
  methods: {
    onSubmit() {
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
    onDeleteCMM: function(index, cmm_id) {
      this.cmms.splice(index, 1)
      console.log(index, cmm_id)
    },
    getCourses() {
      console.log('started method getCourses()')
      const path = 'http://localhost:5000/user-courses'
      axios.get(path).then(
        res => {
          this.courses = res.data.courses
          this.cmms = res.data.cmms
        },
        error => {
          console.error(error)
        },
      this.downloadedCourses = true
      )
    },
    toggleActive(index) {
      if (this.seenCMM.includes(index)) {
        this.seenCMM = this.seenCMM.filter(entry => entry !== index);

        return; 
      }

      this.seenCMM.push(index);
   }
  }
}
</script>
