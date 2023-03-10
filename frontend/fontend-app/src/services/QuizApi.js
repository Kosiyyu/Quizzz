import axios from 'axios';
import {API_BASE_URL} from './config';
import {toast} from 'react-toastify';

export const createQuiz = (data) => {
    return axios.post(`${API_BASE_URL}/api/quizzes`, data, {
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            toast.success('Quiz created successfully!', {
                position: toast.POSITION.BOTTOM_RIGHT
            });
            return response.data;
        })
        .catch(error => {
            toast.error('Error while creating quiz!', {
                position: toast.POSITION.BOTTOM_RIGHT
            });
        });
}

export const getQuizById = (id) => {
    return axios.get(`${API_BASE_URL}/api/quizzes/id/${id}`)
        .then(response => response.data)
        .catch(error => {
            console.log(error);
        });
}

export const getQuizByName = (name) => {
    return axios.get(`${API_BASE_URL}/api/quizzes/name/${name}`)
        .then(response => response.data)
        .catch(error => {
            console.log(error);
        });
}

