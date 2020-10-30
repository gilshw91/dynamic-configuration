import { useState, useEffect } from "react";

export const useFetch = (url) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  //const callApi = async (url, options) => {
  const callApi = (url, options) => {
    if (!url) {
      setError(null);
      setData(null);
      setLoading(false);

      return;
    }
    setLoading(true);

    // DEBUG CODE
    //await new Promise((t) => setTimeout(t, 3000));

    try {
      //const res = await fetch(url, options);
      fetch(url, options).then((res) => {
        if (res.status !== 200) {
          let msg = `${res.message} [${res.status}]`;
          switch (res.status) {
            case 404:
              msg = "Not Found";
              break;
            default:
              break;
          }
          setError(msg);
        } else {
          setError(null);
          res.json().then((json) => setData(json));
        }
      });
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (url) callApi(url);
  }, [url]);
  return [{ data, error, loading }, callApi];
};
