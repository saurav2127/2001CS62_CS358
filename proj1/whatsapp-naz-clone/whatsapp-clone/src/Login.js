import React, { useState } from 'react'
import './Login.css'
import { Button } from '@material-ui/core'
import { auth, provider } from './firebase'
import { useStateValue } from './StateProvider'
import { actionTypes } from './reducer'

function Login() {
    const [{}, dispatch] = useStateValue();

    const signIn = () => {
        auth
            .signInWithPopup(provider)
            .then((result) => {
                dispatch({
                    type: actionTypes.SET_USER,
                    user: result.user,
                })
            })
            .catch((error) => alert(error.message));
    }
  return (
    <div className='login'>
        <div className='login_container'>
            <img 
                src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWq8cUYfuSM9IEiM2_eUojnZTegBWK44kQEQ&usqp=CAU'
                alt=''
            />
            <div className='login_text'>
                <h1>Sign In to Whatsapp</h1>    
            </div>

            <Button onClick={signIn}>
                Sign In with Google
            </Button>
        </div>
    </div>
  )
}

export default Login