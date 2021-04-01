var updateBtns = document.getElementsByClassName('update-cart')
// console.log("hello above for loop")
// console.log(updateBtns.length)
for(var i = 0; i < updateBtns.length; i++){
	// console.log("hello inside for loop")
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		// console.log("hello inside function()")
		console.log('productId:', productId, 'action:', action)
		
		console.log('USER:', user)
		if(user == 'AnonymousUser'){
			console.log('User is not authenticated')
		}
		else{
			// console.log('User is authenticated, sending data...')
			updateUserOrder(productId, action)
		}
	})
}
// console.log("hello below for loop")
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')
	
	var url = 'http://127.0.0.1:8000/index/update_item/'
	
	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'productId': productId, 'action': action}) 
		// this data is send to backend i.e., to views.py
		// as we want to send this data as string we have used stringify
	})
	.then((response) => { 
	// Once the date is sent we return a Promise. To return a promise this
	// is the response that we get after we send the data to this view i.e., updateItem 
		if (!response.ok){
            // error processing
            throw 'Error';
        }
		return response.json();
	})
	// now after we have sent the data to the view and it is processed and everything 
	// went right we want to return this response i.e., 'Item was added' as a Promise
	// to fetch
	.then((data) => { // Promise
		console.log('data:', data)
		if (action == 'add'){
			alert('Item was added')
		}
		if (action == 'remove'){
			alert('Item was removed')
		}
		location.reload() // to reload the page automatically
	})
}