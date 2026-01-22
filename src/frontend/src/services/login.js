import axios from 'axios'
const baseUrl = 'http://127.0.0.1:8000/login/'

const createAccount = newAccount => {
    const request = axios.post(`${baseUrl}create`, newAccount)
    return request.then(response => response.data)
}

const loginAccount = async accountDetails => {
  const params = new URLSearchParams()
  params.append("username", accountDetails.email)
  params.append("password", accountDetails.password)

  const response = await axios.post(
    baseUrl,
    params,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      }
    }
  )

  return response.data
}


export default { createAccount, loginAccount, }