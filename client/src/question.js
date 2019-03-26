import React, { Component  } from 'react'

import Button from 'react-bootstrap/Button'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import './App.css'

class Question extends Component {
  constructor(props) {
    super(props);
    this.state = {
      radio: null,
      loading: true,
      skip: false
    }
    this.timer()
  }
  componentWillReceiveProps () {
    setTimeout(function() { //Start the timer
        this.setState({skip_video: true})
    }.bind(this), 15000)
    this.setState(
      {
        radio: null,
        loading: true,
        skip_video: false
      }
    )
  }
  timer () {
    setTimeout(function() { //Start the timer
        this.setState({loading: false})
    }.bind(this), 8000)

  }

  optionOnClick = (nr) => () => {
    this.setState({
      radio: nr
    })
  }

  submit = event => {
    this.props.onChange(this.state.radio)
    this.setState(
      {
        radio: null,
        loading: true,
        skip_video: false
      }
    )
    this.timer()
  }

  render () {
    // You put files under /client/public/Video
    //     var videoPath = '/Video/' + this.props.videoUID
    // And replace the video with iframe:
    //    <video className="resp-iframe" height="600" key={this.props.videoUID} controls>
    //      <source src={videoPath} type="video/mp4" />
    //    </video>

    // Or on YouTube
    var videoPath = 'https://www.youtube.com/embed/' + this.props.videoUID
    // Change videoUID to a list of videoIDs if necessary
    return (
      <React.Fragment>
        <div className="resp-container">
          <iframe title={videoPath} className='resp-iframe' height="600" src={videoPath} frameborder="0"
                  allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"></iframe>
        </div>
        <p> (This is just a sample video; please put your video A and B in the same video or modify the code to display two videos)</p>
        <br/>
        <p> Which video looks more realistic and consistent? {this.state.radio} </p>
        <Container>
          <Row>
            <Col md={{ span: 1, offset: 5  }}>
            <Button variant="outline-primary" type="submit"
              active={this.state.radio==="A"}
              size="lg"
              bt="padding: 30px 150px"
              onClick={this.optionOnClick("A")}
              checked={this.state.radio==="A" ? true : false}
              disabled={this.state.loading}
            >
              A
            </Button>
            </Col>
            <Col md={{ span: 1}}>
            <Button
              variant="outline-primary" type="submit"
              active={this.state.radio==="B"}
              size="lg"
              onClick={this.optionOnClick("B")}
              checked={this.state.radio==="B" ? true : false}
              disabled={this.state.loading}
            >
              B
            </Button>
            </Col>
          </Row>
          <Row>
            <Col md={{offset: 8}}>
              <Button
                variant="primary"
                type="submit"
                onClick={this.submit}
                disabled={this.state.radio == null ? true : false}
              >
                Next >
              </Button>
            </Col>
          </Row>
          {this.state.skip_video &&
            <Row>
              <Button
                variant="primary"
                type="submit"
                onClick={this.submit}
              >
                Cannot play the video? Click here to skip >
              </Button>
            </Row>
          }
        </Container>
      </React.Fragment>
    )
  }
}

export default Question
