import { createContext, useState, useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import "antd/dist/antd.css";
import axios from "axios";
import Navbar from "./components/Navbar/Navbar";
import Visualisation from "./pages/Visualisation/Visualisation";

export const GraphContext = createContext(null);

function App() {
  const [graph, setGraph] = useState(null);
  const [graphLoading, setGraphLoading] = useState(true);
  const [articleLinks, setArticleLinks] = useState(null);
  const [articleTitles, setArticleTitles] = useState(null);
  const [articleSummaries, setArticleSummaries] = useState(null);
  const [currentNodeTypes, setCurrentNodeTypes] = useState(null);
  const [currentLinkTypes, setCurrentLinkTypes] = useState(null);
  const [dateState, setDateState] = useState(30);
  const [showHowTo, setShowHowTo] = useState(true);
  const nodeStyles = {
    Parent: "#0e1f58",
    Person: "#ffbe09",
    News: "#ff4f79",
    Subsidiary: "#4169e1",
    Shareholder: "#62dce7",
  };

  const reactSelectFormatter = (array) => {
    return array.map((element) => ({
      value: `${element}`,
      label: `${element}`,
    }));
  };

  var production = "https://visualise-news.herokuapp.com/api";
  var development = "http://localhost:5000/api";
  var apiURL = process.env.NODE_ENV === "production" ? production : development;

  useEffect(() => {
    async function queryGraphDB() {
      await axios
        .get(apiURL)
        .then((graph) => {
          setGraph(graph.data);
          setCurrentNodeTypes(
            reactSelectFormatter(
              Array.from(new Set(graph.data.nodes.map((node) => node.label)))
            )
          );
          setCurrentLinkTypes(
            reactSelectFormatter(
              Array.from(
                new Set(graph.data.links.map((link) => link.relationship))
              )
            )
          );
        })
        .catch((err) => console.log(err));
      setGraphLoading(false);
    }
    queryGraphDB();
    async function queryMongoDB() {
      await axios
        .get(apiURL + "/get_article_links")
        .then((res) => {
          const links = Array.from(
            res.data.map((document) => JSON.parse(document).link)
          );
          setArticleLinks(links);
          const titles = Array.from(
            res.data.map((document) => JSON.parse(document).title)
          );
          setArticleTitles(titles);
          const summaries = Array.from(
            res.data.map((document) => JSON.parse(document).short_desc)
          );
          setArticleSummaries(summaries);
        })
        .catch((err) => console.log(err));
    }
    queryMongoDB();
  }, []);

  return (
    <div>
      {graph && (
        <GraphContext.Provider
          value={{
            nodeHook: { currentNodeTypes, setCurrentNodeTypes },
            linkHook: { currentLinkTypes, setCurrentLinkTypes },
            loadingHook: { graphLoading, setGraphLoading },
            graphHook: { graph, setGraph },
            styleHook: { nodeStyles },
            dateHook: { dateState, setDateState },
            articleLinksHook: { articleLinks, setArticleLinks },
            articleTitlesHook: { articleTitles, setArticleTitles },
            articleSummariesHook: { articleSummaries, setArticleSummaries },
            showHowToHook: { showHowTo, setShowHowTo },
          }}
        >
          <Navbar />
          <Routes>
            <Route path="/" element={<Visualisation />} />
          </Routes>
        </GraphContext.Provider>
      )}
    </div>
  );
}

export default App;
