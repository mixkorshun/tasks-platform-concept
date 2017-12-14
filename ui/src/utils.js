export function request(path, options) {
  // todo: remove hardcoded value
  const prefix = 'http://127.0.0.1:5000';

  let url = prefix + path;
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