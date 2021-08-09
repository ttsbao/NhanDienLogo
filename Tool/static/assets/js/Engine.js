    class App extends React.Component {

      constructor(props) {
        super(props);
        this.state = {
          sessions: []
        }
        this.addSession = this.addSession.bind(this);
      }

      addSession() {
        const id = this.state.sessions.length;
        this.setState( state => ({
          sessions: state.sessions.concat( id ),
        }));
      }


      render() {
        return (
          <div>
            <button onClick={this.addSession} >+ Add Session</button>
            <div className="switchers">
              {this.state.sessions.map((x, i) => {
                return <SessionSwitcher index={i + 1}  />;
              })}
            </div>
          </div>
        );
      }
    }

    class SessionSwitcher extends React.Component {
      render() {
        return (
          <div className="switcher">
          </div>
        )
      }
    }

    ReactDOM.render(
      <App />,
      document.querySelector('#app')
    );