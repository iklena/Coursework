import { simulation, atOnceUsers, global, scenario, getParameter } from "@gatling.io/core";
import { http, status } from "@gatling.io/http";
import { constantUsersPerSec, nothingFor, rampUsers, rampUsersPerSec, stressPeakUsers } from "@gatling.io/core"; //"../target/bundle";

export default simulation((setUp) => {
  // Define HTTP configuration

  const httpProtocol = http.baseUrl("https://api.clickup.com").acceptHeader("application/json");

  // Define scenario

  const scenarioForClickUp = scenario("Scenario for ClickUp").exec(
    http("Get Spaces")
      .get("/api/v2/team/90121846530/space")
      .header("Authorization", "pk_302569192_H8G5ELRN8N4VV08M4RN6DPKG52H52YHF")
      .check(status().is(200))
  );

  // Define injection profile and execute the test

  // Report 1 - Навантаження 10 users/sec протягом 20 sec, потім пікове навантаження 100 users/sec на 5 sec і ще 10 users/sec протягом 20 sec
  // setUp(
  //   scenarioForClickUp
  //     .injectOpen(
  //       constantUsersPerSec(10).during(20),
  //       stressPeakUsers(100).during(5),
  //       constantUsersPerSec(10).during(20)
  //     )
  //     .protocols(httpProtocol)
  // );

  // Report 2 - Навантаження 20 users/sec протягом 20 sec, потім ramp up навантаження 100 users/sec на 30 sec
  // setUp(
  //   scenarioForClickUp
  //     .injectOpen(constantUsersPerSec(20).during(20), rampUsers(100).during(30))
  //     .protocols(httpProtocol)
  // );

  // Report for the coursework

  setUp(
    scenarioForClickUp
      .injectOpen(
        nothingFor(3), // 1. сперва 3 секунды ничего не делаем
        atOnceUsers(10), // 2. потом одновременно отправляем запрос от 10 юзеров
        rampUsers(10).during(5), // 3. далее на протяжении 5 секунд увеличиваем на 10 юзеров
        constantUsersPerSec(40).during(10), // 4. потом 10 секунд держим 40 юзеров
        stressPeakUsers(100).during(5), // 5. делаем стресс тест в 100 юзеров на протяжении 5 секунд
        constantUsersPerSec(20).during(10) // 6. потом 10 секунд держим 20 юзеров
      )
      .protocols(httpProtocol)
  );
});