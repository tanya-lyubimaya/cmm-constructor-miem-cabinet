import Mock from 'mockjs'

const data = Mock.mock({
  'items': 'Hello World!!'
})

export default [
  {
    url: '/vue-admin-template/hello/text',
    type: 'get',
    response: config => {
      const items = data.items
      return {
        code: 20000,
        data: {
          total: items.length,
          items: items
        }
      }
    }
  }
]