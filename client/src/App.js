import React, { Component } from 'react'

import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import FormControl from 'react-bootstrap/FormControl'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import './App.css'
import Question from './question'

const fetch = require('isomorphic-fetch')

const INITIAL_STATE = {
  page: 'index',
  surveyID: null,
  videoUIDs: [],
  currentIndex: 0,
  name: ''
}

class App extends Component {
  constructor (props) {
    super(props)
    this.state = INITIAL_STATE
  }
  requestStart = () => {
    let startURL = process.env.REACT_APP_ENDPOINT + '/start_survey/' + this.state.name
    fetch(startURL).then((response) => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error('Something went wrong')
      }
    })
      .then((responseJson) => {
        console.log(responseJson)
        var videoPairs = responseJson.videoPairs
        var videoUIDs = []
        for (let id in videoPairs) {
          videoUIDs.push(videoPairs[id])
        }
        this.setState(
          {
            page: 'survey',
            surveyID: responseJson.ID,
            videoUIDs: videoUIDs
          }
        )
        return responseJson
      })
      .catch((error) => {
        alert("English name please")
        console.log(error)
      })
  }

  setName = e => {
    console.log(e)
    this.setState(
      {
        name: e.target.value
      }
    )
  }

  sendAnswer (uid, answer) {
    let answerURL = process.env.REACT_APP_ENDPOINT + '/answer_question/' + this.state.name + '/'+ uid + '/' + answer
    fetch(answerURL).then((response) => {
      if (response.ok) {
        return response.json()
      } else {
        throw new Error('Something went wrong')
      }
    })
      .then((responseJson) => {
        console.log(responseJson)
      })
      .catch((error) => {
        alert("Error QQ Please report")
        console.log(error)
      })

  }
  nextQuestion (answer) {
    console.log(answer)
    let uid = this.state.videoUIDs[this.state.currentIndex]
    if (answer === 'A' || answer === 'B') {
      this.sendAnswer(uid, answer)
    }
    var newIndex = this.state.currentIndex + 1
    // Finished; refresh
    if (newIndex === this.state.videoUIDs.length) {
      this.setState({page: 'ending'})
      setTimeout(function() { //Start the timer
          this.setState(INITIAL_STATE)
      }.bind(this), 5000)
    }
    else {
       this.setState(
         {
           currentIndex: newIndex
         }
       )

    }
  }
  startSurvey = () => {
    console.log('started')
    this.requestStart()
  }
  indexView () {
    return (
      <React.Fragment>
        {this.title()}
        <Container>
          <Row>
            <Col md={{span: 4, offset: 2}}>
              <Form.Label>
                Please enter your name:
              </Form.Label>
            </Col>
            <Col md={{span: 4}}>
              <FormControl
                placeholder="Name"
                size='lg'
                onChange={this.setName}
              />
            </Col>
          </Row>
        </Container>
        <br/>
        <Button
          onClick={this.startSurvey} disabled={this.state.name === '' ? true : false}
          size='lg'
        >
          Start
        </Button>
      </React.Fragment>
    )
  }
  endingView () {
    return (
      <React.Fragment>
        <h2> Thanks for answering! </h2>
        <h3> Redirect to homepage in 5 seconds .. </h3>
      </React.Fragment>
    )
  }
  title () {
    return (
      <React.Fragment>
        <br />
        <h3> User Study </h3>
        <br />
        <h4> Your Title </h4>
        <br />
        <br />
      </React.Fragment>
    )
  }
  surveyView() {
    let { surveyID, videoUIDs, currentIndex } = this.state
    return (
      <React.Fragment>
        <Container>
          <Row>
            <Col md={{span: 4, offset: 2}}>
              Survey No. {surveyID}
            </Col>
            <Col md={{span: 3}}>
              Question {currentIndex + 1} / {videoUIDs.length}
            </Col>
          </Row>
        </Container>
        <Question videoUID={videoUIDs[currentIndex]} onChange={this.nextQuestion.bind(this)}/>
      </React.Fragment>

    )
  }
  header () {

  }
  view () {
    let { page } = this.state
    switch (page) {
      case 'loading':
        return null
      case 'index':
        return this.indexView()
      case 'ending':
        return this.endingView()
      case 'survey':
        return this.surveyView()
      default:
        return this.indexView()
    }
  }
  render () {
    return (
      <div className='App'>
        <link
          rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
          integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS"
          crossOrigin="anonymous"
        />
        <header className='App-header'>
        </header>
        <div className='App-body'>
          {this.view()}
        </div>
        <footer className='App-footer'>
          Copyright © 2019 Ya-Liang Chang (Allen)
          <a href="https://github.com/amjltc295/CVUserStudyWebsite">
            <img border="10" alt="GitHub" src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="25" height="25" />
          </a>
        </footer>
      </div>
    )
  }
}

export default App
