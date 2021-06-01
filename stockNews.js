/**
 *
 * main() will be run when you invoke this action
 *
 * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
 *
 * @return The output of this action, which must be a JSON object.
 *  
 */
 paramsInput = {
    env_id: "system",
    api_key: "a-pugZwx81CeazpgllKNPgfWxIXBYGgpJj-qsIq4MsVb",
    url:"https://api.us-south.discovery.watson.cloud.ibm.com/instances/d19e700b-3209-4869-a8bb-279a7b7c4e8a",
    collection_id:"news-en",
    input: "Tesla"
 };

 const DiscoveryV1 = require('ibm-watson/discovery/v1');
 const { IamAuthenticator } = require('ibm-watson/auth');


 function getRandomInt(max) {
   return Math.floor(Math.random() * Math.floor(max));
 }
 
 async function main(params) {
    // const discovery = new DiscoveryV1({
    //     version: "2018-12-03",
    //     iam_apikey: params.api_key,
    //     url: params.url,
    // });

    const discovery = new DiscoveryV1({
        version: "2018-12-03",
        authenticator: new IamAuthenticator({
            apikey: params.api_key,
        }),
        url: params.url
    });

    const offset = getRandomInt(50);

    const queryParams = {
        environmentId: params.env_id,
        collectionId: params.collection_id,
        language: "en",
        natural_language_query:
            params.input + " stock",
        count: 1,
        offset: offset
    };
    try {
        data = await discovery.query(queryParams);
        let response = data.result.results.map((v,i) => {
            return `${v.title}
                    ${v.text}
                    ${v.url}`
    });
    return {
        result: response.join("\n\n"),
        // result:data
    };
    } catch (err) {
    return { error: "it failed : " + err };
    }
 }


let userToken = main(paramsInput);
console.log(userToken) // Promise { <pending> }
  
userToken.then(function(result) {
     console.log(result) // "Some User token"
})