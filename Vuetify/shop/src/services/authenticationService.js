import { BehaviorSubject } from 'rxjs';
import axios from 'axios'
import { useToast } from 'vue-toastification'
const toast = useToast()


export const authenticationService = {
    login,
    logout,
    getCurrentUser
};

async function login(email, password) {
    const form = new FormData();
     form.append('username', email);
     form.append('password', password);
     const response = await axios.post('http://localhost:8000/token', form);
     if (response.status == 200) {
        localStorage.setItem('currentUserToken', response.data.access_token);
        await setUserInfo();
        axios.defaults.headers.common = {'Authorization': `bearer ${response.data.access_token}`}
    }
    else {
        toast.error("Произошла ошибка");
    }

}

function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('currentUserToken');
    localStorage.removeItem('user');
    axios.defaults.headers.common = {'Authorization': `bearer `}
}

function getCurrentUser() {
    if (localStorage.getItem('user')) {
        const user = JSON.parse(localStorage.getItem('user'));
        return user;
    }
}

async function setUserInfo() {
    const token = localStorage.getItem('currentUserToken');

    console.log(token);
    const response = await axios.get('http://localhost:8000/users/me', {
        headers: {Authorization: `Bearer ${token}`}
    });

    const user = {
        "userName": response.data.name,
        "userEmail": response.data.email,
        "userId": response.data.id,
        "userRole": response.data.role,
    };
    const parsed = JSON.stringify(user);
    localStorage.setItem('user', parsed);   
}

function handleResponse(response) {
    if (response.status == 200) {
        toast.success("Успешная авторизация!");
        return response.data;
    }
    else {
        toast.error("Произошла ошибка");
    }
}