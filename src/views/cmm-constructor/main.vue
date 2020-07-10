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
        class="button button-outline"
        @click="seen = !seen"
      >Создать КИМ</el-button>

      <div v-if="seen" id="app">
        <el-form id="cmm-name-form" ref="form" :model="form" label-width="120px">
          <el-form-item label="Название КИМа">
            <el-input v-model="form.name" class="input" name="cmm-name" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit" @click="onSubmit">Create</el-button>
            <el-button @click="onCancel">Cancel</el-button>
          </el-form-item>
        </el-form>
        <p>У Вас нет КИМов</p>
      </div>
      <!--
              <br>
                <form action="/main" method="post" novalidate>
                    {{ form.hidden_tag() }}
                        {{ form.cmm_name.label }}
                        {{ form.cmm_name(size=32) }}
                        {% for error in form.cmm_name.errors %}
                            <span style="color: red;">[{{ error }}]</span>
                        {% endfor %}
                    {{ form.submit() }}
                </form>
      {{ form.name(class="form-control", placeholder="Имя", **{'v-model':'user.name'}) }}-->
      <h3 class="title">Мои курсы</h3>
      <ul>
        <li v-for="course of courses" :key="course.courseName">{{ course.courseName }}</li>
      </ul>
      <!--
            <h3 class="title">Мои курсы</h3>
            {% if data.courses %}
                <ul>
                    {% for course in data.courses %}
                        <li class="cmm-name"><a target="_blank" rel="noopener noreferrer" href="{{ course.courseUrl }}">{{ course.courseName }}</a></li>
                    {% endfor %}
                </ul>
            {% else %}
                У вас нет преподаваемых курсов.
            {% endif %}
            </div>
      -->
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        name: ''
      },
      courses: [],
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
      this.$message(JSON.stringify(this.form.name))
      axios
        .post('http://localhost:5000/cmm-name', {
          'cmm-name': JSON.stringify(this.form.name)
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
