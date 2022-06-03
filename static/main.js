//console.log('hello world')
const userForm=document.querySelector('#userForm')
userForm.addEventListener('submit', async e=> {
    e.preventDefault()
    const username=userForm['username'].value
    const password=userForm['password'].value
    const email=userForm['email'].value

    const response= await fetch('api/users',{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        
        body:JSON.stringify({            
            username,
            email,
            password
        })
    })
    const data=await response.json()
    console.log(data)
    userForm.reset();
})