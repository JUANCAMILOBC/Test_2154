/*
Ejecutar en localhost el HTML(limitaciones de la API free)
*/
const get_news=async()=>{
	let categoria = document.querySelector("#Category").value;

	const apikey="f0d65d4fa5e4490099d5e9b356eba4c6"
	const url=`https://newsapi.org/v2/top-headlines?country=us&category=${categoria}&apikey=${apikey}`;
	console.log(url);

	
	const repuesta=await fetch(url);
	const resultado=await repuesta.json();
	console.log(resultado);

	let news = resultado.articles;

	let listNEWSHTML = ``;

	news.map(noticia=>{
		const{urlToImage, url, title, description, source}=noticia;

		let imagen = (urlToImage)? `<div class="card-image">
									<img src="${urlToImage}" alt=${title}>
									<span class="card-title">${source.name}</span>
									</div>`:null;

		listNEWSHTML += `<div class="col s12 m6 14">
							<div class="card">
							${imagen}
								<div class="card-content">
									<h3>${title}</h3>
									<p>${description}</p>
								</div>
								<div class="card-action">
									<a href="${url}"
									target="_blank"
									rel+"nooper noreferrer"
									class="waves-efect waves-light btn">
									View news complet</a>
								</div>
							</div>
						</div>`;
	});

	let divlistnews = document.querySelector("#divlistnews");
	divlistnews.innerHTML = `<div style="text-align:center">
									<img src="loading.gif" width=300 height=300>
								</div>`;
	setTimeout(()=>{
		divlistnews.innerHTML=listNEWSHTML;
	},3000);
}