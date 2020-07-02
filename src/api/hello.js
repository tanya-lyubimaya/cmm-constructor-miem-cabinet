import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/vue-admin-template/hello/text',
    method: 'get',
    params
  })
}
