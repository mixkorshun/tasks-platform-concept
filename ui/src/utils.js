export function request(path, options) {
  let url = api_endpoint + path;
  if (options.qs) {
    url += '?' + encodeQueryParam(options.qs);
  }

  return fetch(url, options);
}

function encodeQueryParam(params) {
  return Object.keys(params)
    .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
    .join('&');
}